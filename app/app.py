from flask import Flask, jsonify, request
import socket
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentation
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import logging
from elasticapm.contrib.flask import ElasticAPM
from prometheus_client import Counter, Histogram, generate_latest
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize tracing with OpenTelemetry
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Elastic APM configuration
app = Flask(__name__)
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'flask-app',
    'SERVER_URL': 'http://flask-apm:8200',
    'ENVIRONMENT': 'production'
}
apm = ElasticAPM(app)

# Prometheus metrics
metrics = PrometheusMetrics(app)
REQUEST_COUNT = Counter(
    'flask_request_count', 
    'Total request count of the app'
)
REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds', 
    'Request latency in seconds'
)

FlaskInstrumentation().instrument_app(app)

# Add request logging middleware
@app.before_request
def log_request_info():
    logger.info(f'Request: {request.method} {request.url}')
    logger.debug(f'Headers: {dict(request.headers)}')
    logger.debug(f'Body: {request.get_data()}')

@app.after_request
def log_response_info(response):
    logger.info(f'Response: {response.status}')
    logger.debug(f'Response data: {response.get_data()}')
    return response

@app.route('/health')
def health_check():
    logger.info('Health check endpoint called')
    return jsonify({"status": "healthy"})

@app.route('/metrics')
def metrics_endpoint():
    logger.info('Metrics endpoint called')
    return generate_latest()

@app.route('/info')
def info():
    logger.info('Info endpoint called')
    return jsonify({
        "app": "DevOps Project",
        "version": "1.0.0"
    })

@app.route('/')
def hello():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("hello_operation") as span:
        hostname = socket.gethostname()
        span.set_attribute("hostname", hostname)
        logger.info(f'Hello endpoint called from {hostname}')
        
        # Prometheus request count and latency
        REQUEST_COUNT.inc()
        start_time = time.time()
        response = {"message": "Hello from the DevOps Project!", "hostname": hostname}
        REQUEST_LATENCY.observe(time.time() - start_time)

        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
