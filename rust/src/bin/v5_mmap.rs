use std::fs::File;

use memmap2::Mmap;
use rustc_hash::FxHashMap;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let true_values_path = "true_values.txt";
    let file_path = std::env::args().nth(1).expect("Missing file path");

    let file = File::open(file_path)?;
    let map: Mmap = unsafe { Mmap::map(&file).unwrap() };

    let mut tracker = FxHashMap::default();

    for line in map.split(|&c| c == b'\n') {
        let mut parts = line.splitn(2, |&c| c == b';');
        let city = parts.next().unwrap();
        match parts.next() {
            Some(raw_temp) => {
                let temp = rbc::utils::parse_temp(raw_temp);
                tracker
                    .entry(city)
                    .or_insert(rbc::utils::TemperatureTrackerI64::new(temp, temp, temp, 1))
                    .update(temp)
            }
            None => continue,
        }
    }

    let mut tracker_keys: Vec<&[u8]> = tracker.keys().map(|k| *k).collect();
    tracker_keys.sort();

    let mut res: Vec<(String, String, String, String)> = vec![];
    for k in tracker_keys {
        let v = tracker.get(k).unwrap();
        res.push((
            std::str::from_utf8(k).unwrap().to_string(),
            format!("{:.1}", v.min_val as f64 / 10.0),
            format!("{:.1}", v.max_val as f64 / 10.0),
            format!("{:.1}", (v.sum as f64 / v.count as f64) / 10.0),
        ));
    }

    rbc::utils::check_true_values(true_values_path, res);

    // let res = tracker
    //     .iter()
    //     .map(|(k, v)| {
    //         (
    //             std::str::from_utf8(k).unwrap().to_string(),
    //             v.min_val.to_string(),
    //             v.max_val.to_string(),
    //             format!("{:.1}", v.sum / v.count as i64),
    //         )
    //     })
    //     .collect::<Vec<_>>();
    //
    // rbc::utils::check_true_values(true_values_path, res);

    Ok(())
}
