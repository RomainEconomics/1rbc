use rayon::prelude::*;
use rustc_hash::FxHashMap;
use std::{
    fs::File,
    io::{self, Error, Read, Seek},
};

#[derive(Debug)]
struct TemperatureTracker {
    min_val: f64,
    max_val: f64,
    sum: f64,
    count: u64,
}

impl TemperatureTracker {
    fn new(min_val: f64, max_val: f64, sum: f64, count: u64) -> Self {
        Self {
            min_val,
            max_val,
            sum,
            count,
        }
    }

    fn update(&mut self, temp: f64) {
        self.min_val = temp.min(self.min_val);
        self.max_val = temp.max(self.max_val);
        self.sum += temp;
        self.count += 1;
    }

    fn merge(&mut self, city_temp: &TemperatureTracker) {
        self.min_val = city_temp.min_val.min(self.min_val);
        self.max_val = city_temp.max_val.max(self.max_val);
        self.sum += city_temp.sum;
        self.count += city_temp.count;
    }
}

fn find_chunk_boundaries(filename: &String, num_workers: u64) -> io::Result<Vec<(u64, u64)>> {
    let mut file = File::open(filename).unwrap();

    let file_size = file.metadata().unwrap().len();
    let chunk_size = file_size / num_workers;

    let mut chunks: Vec<_> = Vec::new();

    fn find_new_line(file: &mut File, start: u64) -> u64 {
        file.seek(io::SeekFrom::Start(start)).unwrap();
        let mut buffer = [0; 2048];

        let n = file.read(&mut buffer).unwrap();
        if n == 0 {
            return file.stream_position().unwrap();
        }

        let pos = buffer.iter().position(|&b| b == b'\n').unwrap();
        start + pos as u64
    }

    let mut start = 0;
    for _ in 0..num_workers {
        let mut end = find_new_line(&mut file, start + chunk_size);
        end = file_size.min(end);
        chunks.push((start, end));
        start = end;
    }

    Ok(chunks)
}

fn process_chunk(
    filename: &String,
    start: u64,
    end: u64,
) -> Result<FxHashMap<Vec<u8>, TemperatureTracker>, Error> {
    let mut file = File::open(filename)?;
    file.seek(io::SeekFrom::Start(start)).unwrap();

    let buffer_size = (end - start - 1) as usize;

    let mut buf = vec![0u8; buffer_size];

    file.read_exact(&mut buf)?;

    let mut tracker = FxHashMap::default();

    for line in buf.split(|&x| x == b'\n') {
        let sep = line.iter().position(|&c| c == b';');

        if let Some(sep) = sep {
            let city = &line[..sep];
            let temp = fast_float::parse::<f64, _>(&line[sep + 1..]).expect("Invalid temperature");
            tracker
                .entry(city.to_vec())
                .or_insert(TemperatureTracker::new(temp, temp, temp, 1))
                .update(temp)
        }
    }

    Ok(tracker)
}

fn main() {
    let true_values_path = "true_values.txt";
    let file_path = std::env::args().nth(1).expect("Missing file path");
    let num_workers = std::env::args()
        .nth(2)
        .expect("Missing number of workers")
        .parse::<u64>()
        .expect("Invalid number of workers");

    let chunks = find_chunk_boundaries(&file_path, num_workers).unwrap();

    let mut tracker: FxHashMap<String, TemperatureTracker> = FxHashMap::default();

    let temp_res: Vec<FxHashMap<Vec<u8>, TemperatureTracker>> = chunks
        .par_iter()
        .map(|&(start, end)| process_chunk(&file_path, start, end).unwrap())
        .collect();

    for res in temp_res {
        for (k, v) in res.iter() {
            let city = std::str::from_utf8(k).expect("Invalid UTF-8").to_string();
            tracker
                .entry(city)
                .or_insert(TemperatureTracker::new(
                    v.min_val, v.max_val, v.sum, v.count,
                ))
                .merge(v)
        }
    }

    let mut tracker_keys: Vec<&String> = tracker.keys().collect();
    tracker_keys.sort();

    let mut res: Vec<(String, String, String, String)> = vec![];
    for k in tracker_keys {
        let v = tracker.get(k).unwrap();
        res.push((
            k.to_string(),
            format!("{:.1}", v.min_val),
            format!("{:.1}", v.max_val),
            format!("{:.1}", (v.sum / v.count as f64)),
        ));
    }

    rbc::utils::check_true_values(true_values_path, res);
}
