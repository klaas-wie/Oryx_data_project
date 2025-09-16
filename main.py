from html_parser import parse_oryx_html
from write_csv import write_losses_csv

def main():
    losses = parse_oryx_html()
    write_losses_csv(losses)

if __name__ == "__main__":
    main()