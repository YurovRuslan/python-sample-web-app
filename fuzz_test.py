import atheris
import sys
import json
from app import app

@atheris.instrument_func
def test_input(data):
    fdp = atheris.FuzzedDataProvider(data)
    input_str = fdp.ConsumeString(100)

    with app.test_client() as client:
        try:
            response = client.post('/post', json={'input': input_str})
            if response.status_code not in [200, 400]:
                raise RuntimeError(f"Unexpected status code: {response.status_code}")
        except ZeroDivisionError:
            raise  # Мы хотим, чтобы фаззер обнаружил эту ошибку
        except json.JSONDecodeError:
            pass  # Игнорируем неверный JSON
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

def main():
    atheris.Setup(sys.argv, test_input)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
