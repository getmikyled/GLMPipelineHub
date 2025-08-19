# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import sqlite3
import json
import logging
from contextlib import ContextDecorator

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, Span
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult, BatchSpanProcessor
from opentelemetry.trace import get_tracer

DATABASE_PATH = 'traces.db'

database = sqlite3.connect(DATABASE_PATH)

class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_schema()

    def _initialize_schema(self):
        """Create the spans table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS spans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trace_id TEXT,
                    span_id TEXT,
                    parent_span_id TEXT,
                    name TEXT,
                    start_time INTEGER,
                    end_time INTEGER,
                    attributes TEXT
                )
            """)
            conn.commit()

    def export(self, spans: list):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for span in spans:
                    cursor.execute("""
                        INSERT INTO spans (
                            trace_id, span_id, parent_span_id,
                            name, start_time, end_time, attributes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        str(span.context.trace_id),
                        str(span.context.span_id),
                        str(span.parent.span_id) if span.parent else None,
                        span.name,
                        span.start_time,
                        span.end_time,
                        json.dumps(dict(span.attributes))
                    ))
                conn.commit()
            return SpanExportResult.SUCCESS
        except Exception as e:
            print(f"[SQLiteSpanExporter] Export failed: {e}")
            return SpanExportResult.FAILURE

    def shutdown(self):
        pass

class TraceLogger(logging.Logger):
    """ A custom logger used for adding logs to the current span."""

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        """ Overrides the existing _log() method to implement span tracing for logs."""
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

        parent_span = trace.get_current_span()
        if parent_span and parent_span.is_recording():
            tracer = get_tracer(__name__)

            log_name = f"{logging.getLevelName(level)}: {msg % args}"

            # Create short-lived child span
            with StartSpan(log_name) as log_span:
                # Force it to inherit the parent span
                log_span.set_attribute("log", True)
                log_span.set_attribute("level", logging.getLevelName(level))
                log_span.set_attribute("message", msg % args)

class StartSpan(ContextDecorator):

    def __init__(self, name : str):
        """ Initialize the context decorator.

        Args:
            name (str): The name of the span.
        """

        self.name = name
        self._span = None
        self._context = None
        self._tracer = trace.get_tracer(__name__)

    def __enter__(self):
        """ Start the span on enter."""
        self._context = self._tracer.start_as_current_span(self.name)
        self._span = self._context.__enter__()
        return self._span

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit."""
        return self._context.__exit__(exc_type, exc_val, exc_tb)

# Setup tracer provider
provider = TracerProvider()
trace.set_tracer_provider(provider)

# Add File Exporter
span_exporter = SQLiteSpanExporter('traces.db')
provider.add_span_processor(BatchSpanProcessor(span_exporter))

# Setup logger
logging.setLoggerClass(TraceLogger)
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('glm')

def get_logger():
    logging.setLoggerClass(TraceLogger)
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger('glm')