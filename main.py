import GTMetrix
import argparse
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="GTMetrixRecommendation")
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="The url of the page")
    parser.add_argument(
        "-o", "--output_file", help="the file to save the recommendations to", type=str, default="recommendations.txt")
    parser.add_argument(
        "-l", "--limit", help="The number of recommendations to display", type=int, default=6)
    parser.add_argument(
        "-v", "--verbose", help="Display debug message", action="store_true")
    args = parser.parse_args()
    email = "jose.colella@dynatrace.com"
    apiToken = "43b7a445ee75fefe746e603d2bf783c2"
    gtMetrix = GTMetrix.GTMetrixAPI(email, apiToken)
    gtMetrix.requestTest(args.url)
    logging.info("The test is being processed")
    try:
        gtMetrix.getTestResults()
        time.sleep(16)
        gtMetrix.getTestResults()
    except KeyError:
        # If the test is still in queue
        time.sleep(16)
        gtMetrix.getTestResults()
    logging.info("Saving to file")
    gtMetrix.savePageSpeedRecommendations(args.output_file, args.limit)
