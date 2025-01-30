from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import httpx
import asyncio

app = Flask(__name__)


@app.route("/health")
def health():
    """Health endpoint that returns a simple status."""
    return {"status": "ok"}


async def perform_health_check():
    """Async function to perform the health check using HTTPX."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.mystiko.harshallaheri.me/health-check", timeout=10
            )
            print(f"Health check completed. Status code: {response.status_code}")
            return response.status_code
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return None


def scheduled_health_check():
    """Wrapper function to run the async health check."""
    asyncio.run(perform_health_check())


# Configure and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_health_check, "interval", minutes=1)
scheduler.start()

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5678)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
