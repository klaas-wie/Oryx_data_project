import csv

def write_losses_csv(losses, filename="losses.csv"):
    """Write a list of loss dictionaries to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "equipment_type", "category", "loss_type",
            "link_type", "link", "date"
        ])
        for loss in losses:
            writer.writerow([
                loss["equipment_type"],
                loss["category"],
                loss["loss_type"],
                loss["link_type"],
                loss["link"],
                loss.get("date", "")
            ])

