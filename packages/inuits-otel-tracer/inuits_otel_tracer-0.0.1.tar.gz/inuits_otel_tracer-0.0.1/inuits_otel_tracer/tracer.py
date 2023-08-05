# Class for using OTel tracing

import os
from typing import Optional, Sequence
from grpc import ChannelCredentials, Compression
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter      

# SDK libraries 
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider

class Tracer:
    def __init__(self, serviceName, currentFileName):
        self.serviceName = serviceName
        self.currentFileName = currentFileName
    
    def configTracer(
        self, 
        isInsecure: Optional[bool] = None, 
        credentials: Optional[ChannelCredentials] = None, 
        headers: Optional[Sequence] = None, 
        timeout: Optional[int] = None, 
        compression: Optional[Compression] = None
    ):
        OTLPSpan_exporter = OTLPSpanExporter(  
            endpoint = os.getenv("OTLP_EXPORTER_ENDPOINT", "otel-collector:4317"),   
            insecure = isInsecure,
            credentials = credentials,
            headers = headers,
            timeout = timeout,
            compression = compression
        )   

        trace.set_tracer_provider(
            TracerProvider(
                resource=Resource.create({SERVICE_NAME: f"{self.serviceName}"})
            )
        )

        self.OTLPSpanExporter = OTLPSpan_exporter


