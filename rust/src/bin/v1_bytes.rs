use std::io::Read;
use std::{collections::HashMap, fs::File};

use rbc::utils::TemperatureTrackerF64;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let true_values_path = "true_values.txt";
    let file_path = std::env::args().nth(1).expect("Missing file path");

    let mut buf = vec![];

    {
        let mut file = File::open(file_path)?;
        file.read_to_end(&mut buf)?;
        assert!(buf.pop() == Some(b'\n'));
    }

    let mut tracker = HashMap::new();

    for line in buf.split(|&c| c == b'\n') {
        let mut parts = line.splitn(2, |&c| c == b';');
        let city = parts.next().unwrap();
        let temp = parts.next().unwrap();
        let temp = unsafe { std::str::from_utf8_unchecked(temp) }
            .parse::<f64>()
            .unwrap();

        tracker
            .entry(city)
            .or_insert(TemperatureTrackerF64::new(temp, temp, temp, 1))
            .update(temp)
    }

    let mut tracker_keys: Vec<&[u8]> = tracker.keys().map(|k| *k).collect();
    tracker_keys.sort();

    let mut res: Vec<(String, String, String, String)> = vec![];
    for k in tracker_keys {
        let v = tracker.get(k).unwrap();
        res.push((
            std::str::from_utf8(k).unwrap().to_string(),
            format!("{:.1}", v.min_val),
            format!("{:.1}", v.max_val),
            format!("{:.1}", v.sum / v.count as f64),
        ));
    }

    rbc::utils::check_true_values(true_values_path, res);

    Ok(())
}
