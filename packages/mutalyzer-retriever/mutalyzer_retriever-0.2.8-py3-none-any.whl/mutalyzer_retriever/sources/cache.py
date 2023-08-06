import gc
import json
import pickle
import time

import matplotlib.pyplot as plt
import orjson
import rapidjson
import redis
import ujson
from pymemcache.client.base import Client

import mutalyzer_retriever.configuration
from mutalyzer_retriever.retriever import retrieve_model, retrieve_model_from_file

# references = ["NG_012337.3"]
# references = ["NC_000024.10", "NG_012337.3"]
references = ["NC_000002.12", "NC_000015.10", "NC_000024.10", "NG_012337.3"]


def _make_pickle_files():
    for reference in references:
        with open(f"references_temp/{reference}") as json_file:
            model_file_json = json.load(json_file)
        with open(f"references_temp/{reference}.pickle", "wb") as pickle_file:
            pickle.dump(model_file_json, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)


def _raw_source():
    summary = {"Time (ns)": {}, "Features (#)": {}, "Sequence sizes": {}}

    for reference in references:
        print(f"\n{reference}")
        t = time.time()
        try:
            m = retrieve_model(reference, timeout=10)
        except Exception as e:
            print(e)
        summary["Time (ns)"][reference] = time.time() - t
        summary["Features (#)"][reference] = len(m["annotations"]["features"])
        summary["Sequence sizes"][reference] = len(m["sequence"]["seq"])

    print(summary)
    fig, axs = plt.subplots(1, 3, figsize=(30, 15))
    for i, k in enumerate(summary):
        labels = []
        values = []
        for reference in summary[k]:
            labels.append(reference)
            values.append(summary[k][reference])
        t = axs[i].bar(labels, values)
        axs[i].set_title(k)
        # axs[i].set_ylabel(k)
        axs[i].bar_label(t, fmt="%d")
    plt.tight_layout()
    plt.savefig("raw_overview.svg")
    plt.show()


def _redis_set():
    conn = redis.Redis("localhost")
    for reference in references:
        with open(f"references_temp/{reference}") as json_file:
            model_json = ujson.load(json_file)

        conn.set(reference + "pickle", pickle.dumps(model_json))
        conn.set(reference + "json", json.dumps(model_json))


def _memcached_set():
    client = Client(("localhost", 11211))
    for reference in references:
        with open(f"references_temp/{reference}") as json_file:
            model_json = ujson.load(json_file)

        client.set(reference + "pickle", pickle.dumps(model_json))
        client.set(reference + "json", json.dumps(model_json))


def _time_comparison():
    conn = redis.Redis("localhost")
    client = Client(("localhost", 11211))

    summary = {}

    N = 20
    for i in range(N):
        print(f"----------\n{i}\n---------")
        for reference in references:
            gc.collect()
            times = {}
            print(f"\n{reference}")
            # t = time.time()
            # try:
            #     m = retrieve_model(reference, timeout=10)
            # except Exception as e:
            #     print(e)
            # times["from_source"] = time.time() - t

            paths = [
                f"references_temp/{reference}.gff3",
                f"references_temp/{reference}.fasta",
            ]

            # t = time.time()
            # model = retrieve_model_from_file(paths)
            # times["from_raw_files"] = time.time() - t
            # gc.collect()

            # conn.set(reference,  orjson.dumps(model))

            t = time.time()
            with open(f"references_temp/{reference}") as json_file:
                model_file_json = json.load(json_file)
            times["file_json"] = time.time() - t
            gc.collect()

            t = time.time()
            with open(f"references_temp/{reference}.pickle", "rb") as pickle_file:
                model_file_pickle = pickle.load(pickle_file)
            times["file_pickle"] = time.time() - t
            gc.collect()

            t = time.time()
            with open(f"references_temp/{reference}") as json_file:
                model_file_ujson = ujson.load(json_file)
            times["file_ujson"] = time.time() - t
            gc.collect()

            t = time.time()
            model_redis_pickle = pickle.loads(conn.get(reference + "pickle"))
            times["redis_pickle"] = time.time() - t
            gc.collect()

            t = time.time()
            model_redis_json = json.loads(conn.get(reference + "json"))
            times["redis_json"] = time.time() - t
            gc.collect()

            t = time.time()
            model_redis_ujson = ujson.loads(conn.get(reference + "json"))
            times["redis_ujson"] = time.time() - t
            gc.collect()

            t = time.time()
            model_redis_orjson = orjson.loads(conn.get(reference + "json"))
            times["redis_orjson"] = time.time() - t
            gc.collect()

            t = time.time()
            model_memcached_pickle = pickle.loads(client.get(reference + "pickle"))
            times["memcached_pickle"] = time.time() - t
            gc.collect()

            t = time.time()
            model_memcached_json = json.loads(client.get(reference + "json"))
            times["memcached_json"] = time.time() - t
            gc.collect()

            t = time.time()
            model_memcached_ujson = ujson.loads(client.get(reference + "json"))
            times["memcached_ujson"] = time.time() - t
            gc.collect()

            t = time.time()
            model_memcached_orjson = orjson.loads(client.get(reference + "json"))
            times["memcached_orjson"] = time.time() - t
            gc.collect()

            for t in times:
                print(f"- {t}: {times[t]}")

            # assert model_file_json == model
            assert model_file_pickle == model_file_json
            assert model_file_ujson == model_file_json
            assert model_redis_pickle == model_file_json
            assert model_redis_orjson == model_file_json
            assert model_redis_pickle == model_file_json
            assert model_redis_json == model_file_json
            assert model_redis_ujson == model_file_json
            assert model_redis_orjson == model_file_json
            assert model_memcached_pickle == model_file_json
            assert model_memcached_json == model_file_json
            assert model_memcached_ujson == model_file_json
            assert model_memcached_orjson == model_file_json

            if reference not in summary:
                summary[reference] = times
            else:
                for k in summary[reference]:
                    summary[reference][k] += times[k]
            gc.collect()

    for reference in summary:
        for k in summary[reference]:
            summary[reference][k] /= N

    fig, axs = plt.subplots(1, len(summary), figsize=(30, 10))

    for i, reference in enumerate(summary):
        print(list(summary[reference].keys()))
        print(list(summary[reference].values()))
        labels = []
        values = []
        for k in summary[reference]:
            labels.append(k)
            values.append(summary[reference][k])
        t = axs[i].bar(labels, values)
        axs[i].set_title(reference)
        axs[i].set_ylabel("Time (ns)")
        axs[i].bar_label(t)
        axs[i].tick_params(labelrotation=90)
    plt.tight_layout()
    plt.savefig("timing.svg")
    plt.show()


def _redis_info():
    conn = redis.Redis("localhost")
    print(json.dumps(conn.info(), indent=2))


if __name__ == "__main__":
    # _raw_source()
    # _make_pickle_files()
    # _redis_set()
    # _memcached_set()
    _time_comparison()
    # _redis_info()
