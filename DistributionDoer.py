class DistributionDoer:

    def __init__(self) -> None:
        super().__init__()

    def output_distribution(self, IP, key, IP_to_data):
        vars = [i for i in dir(IP_to_data) if not callable(i)]
        for x in IP_to_data[IP]
