"""
Python demo showing how to use the MLPerf Inference load generator bindings.
"""

from __future__ import print_function
from absl import app
import mlperf_loadgen
import threading
import time
import numpy


def load_samples_to_ram(query_samples):
    return


def unload_samples_from_ram(query_samples):
    return


def process_query_async(query_samples):
    time.sleep(.001)
    responses = []
    for s in query_samples:
        responses.append(mlperf_loadgen.QuerySampleResponse(s.id, 0, 0))
    mlperf_loadgen.QuerySamplesComplete(responses)


def issue_query(query_samples):
    threading.Thread(
            target=process_query_async,
            args=[query_samples]).start()


def process_latencies(latencies_ns):
    print("Average latency: ")
    print(numpy.mean(latencies_ns))
    print("Median latency: ")
    print(numpy.percentile(latencies_ns, 50))
    print("90 percentile latency: ")
    print(numpy.percentile(latencies_ns, 90))


def main(argv):
    settings = mlperf_loadgen.TestSettings()
    settings.scenario = mlperf_loadgen.TestScenario.Server
    settings.mode = mlperf_loadgen.TestMode.PerformanceOnly
    settings.server_target_qps = 100
    settings.enable_spec_overrides = True
    settings.override_target_latency_ns = 100000000
    settings.override_min_query_count = 100
    settings.override_min_duration_ms = 10000

    sut = mlperf_loadgen.ConstructSUT(issue_query, process_latencies)
    qsl = mlperf_loadgen.ConstructQSL(
        1024, 128, load_samples_to_ram, unload_samples_from_ram)
    mlperf_loadgen.StartTest(sut, qsl, settings)
    mlperf_loadgen.DestroyQSL(qsl)
    mlperf_loadgen.DestroySUT(sut)


if __name__ == '__main__':
    app.run(main)
