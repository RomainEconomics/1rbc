use std::io::{self, BufRead};
use std::{collections::HashMap, fs::File};

use rbc::utils::TemperatureTrackerF64;

type Record = (String, f64);

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let true_values_path = "true_values.txt";
    let file_path = std::env::args().nth(1).expect("Missing file path");

    let file = File::open(file_path)?;
    let lines = io::BufReader::new(file).lines();

    let mut tracker: HashMap<String, TemperatureTrackerF64> = HashMap::new();

    for line in lines.flatten() {
        let (city, temp): (&str, &str) = line.split_once(';').unwrap();
        let record: Record = (city.to_string(), temp.parse::<f64>().unwrap());

        tracker
            .entry(record.0)
            .or_insert(TemperatureTrackerF64::new(record.1, record.1, record.1, 1))
            .update(record.1);
    }

    let mut res = tracker
        .iter()
        .map(|(k, v)| {
            (
                k.to_string(),
                v.min_val.to_string(),
                v.max_val.to_string(),
                format!("{:.1}", v.sum / v.count as f64),
            )
        })
        .collect::<Vec<_>>();

    res.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    rbc::utils::check_true_values(true_values_path, res);

    Ok(())
}
