import csv

def write_losses_csv(losses, filename="most_recent_losses.csv"):
    """Write a list of loss dictionaries to a CSV file.
    Always includes 'manually_changed' column set to False by default.
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "equipment_type", "category", "loss_type",
            "link_type", "link", "date", "manually_changed"
        ])
        for loss in losses:
            writer.writerow([
                loss["equipment_type"],
                loss["category"],
                loss["loss_type"],
                loss["link_type"],
                loss["link"],
                loss.get("date", ""),
                False 
            ])
