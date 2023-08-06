import requests
import typer

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

app = typer.Typer(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)


@app.command()
def get(
    metric: str = "temperature",
    latitude: float = 40.71,
    longitude: float = -74.01,
):
    """Get the weather from latitude and longitude"""
    r = requests.get(
        f"""https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"""
    )
    if r.status_code == 200:
        if metric in r.json()["current_weather"]:
            print(r.json()["current_weather"][metric])
        else:
            print("Metric not supported!")
    else:
        print("Open-Meteo is down!")


@app.command()
def otro_comando():
    """Solo para que muestre la ayuda"""
    print("Hola mundo")


def main():
    app()


if __name__ == "__main__":
    main()
