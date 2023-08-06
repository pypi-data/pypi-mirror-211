from neuralpit.services.api import NeuralPitAPIService
from neuralpit.services.converter import TikaConverterService
import os


def main():
   client = NeuralPitAPIService()
   user = client.getUserProfile()
   print(user)


if __name__ == "__main__":
    main()
