use std::{
    io::{self, BufRead},
    iter::zip,
};

use rustc_hash::FxHashMap;

// Helper to check if the output is correct

pub fn check_true_values(file_path: &str, res: Vec<(String, String, String, String)>) -> bool {
    let file = std::fs::File::open(file_path).unwrap();
    let lines = io::BufReader::new(file)
        .lines()
        .map(|line| line.unwrap())
        .collect::<Vec<_>>();

    for (line, record) in zip(lines, res) {
        let true_values = line.split(';').collect::<Vec<&str>>();
        if true_values[0] != record.0
            || true_values[1] != record.1
            || true_values[2] != record.2
            || true_values[3] != record.3
        {
            println!("Expected: {:?}", true_values);
            println!("Got: {:?}", record);
            return false;
        }
    }
    println!("All values are correct!");
    true
}

// For F64 only

#[derive(Debug)]
pub struct TemperatureTrackerF64 {
    pub min_val: f64,
    pub max_val: f64,
    pub sum: f64,
    pub count: u64,
}

impl TemperatureTrackerF64 {
    pub fn new(min_val: f64, max_val: f64, sum: f64, count: u64) -> Self {
        Self {
            min_val,
            max_val,
            sum,
            count,
        }
    }

    pub fn update(&mut self, temp: f64) {
        self.min_val = temp.min(self.min_val);
        self.max_val = temp.max(self.max_val);
        self.sum += temp;
        self.count += 1;
    }
}

// Use for better output formatting

pub fn format_output_f64(
    tracker: FxHashMap<&[u8], TemperatureTrackerF64>,
) -> Vec<(String, f64, f64, f64)> {
    let mut res = tracker
        .iter()
        .map(|(&k, v)| {
            let city = std::str::from_utf8(k).expect("Invalid UTF-8").to_string();
            (city, v.min_val, v.max_val, v.sum / v.count as f64)
        })
        .collect::<Vec<_>>();

    res.sort_by(|a, b| a.0.cmp(&b.0));
    res
}

pub fn display_output_f64(res: Vec<(String, f64, f64, f64)>) {
    for (city, min_val, max_val, mean_val) in res {
        println!(
            "{}: min = {}, max = {}, mean = {:.2}",
            city, min_val, max_val, mean_val
        )
    }
}

/*
*
*
*
*
*
*
*/

#[derive(Debug)]
pub struct TemperatureTrackerI64 {
    pub min_val: i64,
    pub max_val: i64,
    pub sum: i64,
    pub count: u64,
}

impl TemperatureTrackerI64 {
    pub fn new(min_val: i64, max_val: i64, sum: i64, count: u64) -> Self {
        Self {
            min_val,
            max_val,
            sum,
            count,
        }
    }

    pub fn update(&mut self, temp: i64) {
        self.min_val = temp.min(self.min_val);
        self.max_val = temp.max(self.max_val);
        self.sum += temp;
        self.count += 1;
    }
}

// Custom parsing function for temperature
pub fn parse_temp(raw_temp: &[u8]) -> i64 {
    match raw_temp {
        [b'-', a, b, b'.', c] => {
            -((a - b'0') as i64 * 100 + (b - b'0') as i64 * 10 + (c - b'0') as i64)
        }
        [b'-', a, b'.', c] => -((a - b'0') as i64 * 10 + (c - b'0') as i64),
        [a, b'.', b] => (a - b'0') as i64 * 10 + (b - b'0') as i64,
        [a, b, b'.', c] => (a - b'0') as i64 * 100 + (b - b'0') as i64 * 10 + (c - b'0') as i64,
        _ => panic!("Invalid temperature"),
    }
}

// Use for better output formatting

pub fn format_output_i64(
    tracker: FxHashMap<&[u8], TemperatureTrackerI64>,
) -> Vec<(String, i64, i64, i64)> {
    let mut res = tracker
        .iter()
        .map(|(&k, v)| {
            let city = std::str::from_utf8(k).expect("Invalid UTF-8").to_string();
            (city, v.min_val, v.max_val, v.sum / v.count as i64)
        })
        .collect::<Vec<_>>();

    res.sort_by(|a, b| a.0.cmp(&b.0));
    res
}

pub fn display_output_i64(res: Vec<(String, i64, i64, i64)>) {
    for (city, min_val, max_val, mean_val) in res {
        println!(
            "{}: min = {}, max = {}, mean = {:.2}",
            city, min_val, max_val, mean_val
        )
    }
}
