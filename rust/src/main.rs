use std::fs::File;

// type Record = (String, f64);

// struct TemperatureTracker {
//     min: f64,
//     max: f64,
//     sum: f64,
//     count: u64,
// }

// ./target/release/rust  101,56s user 4,38s system 99% cpu 1:46,43 total
fn main() -> Result<(), Box<dyn std::error::Error>> {
    // let file_path = "../sample.csv";
    println!("Start reading file");

    let file_path = "../../../playground/one_billion_rows/measurements.txt";
    let file = File::open(file_path)?;

    let file_size = file.metadata()?.len();
    println!("{}", file_size);

    Ok(())

    //     let mut rdr = csv::ReaderBuilder::new()
    //         .delimiter(b';')
    //         .from_path(file_path)?;
    //
    //     let mut tracker: HashMap<String, TemperatureTracker> = HashMap::new();
    //
    //     let mut n = 0;
    //
    //     for result in rdr.deserialize() {
    //         let record: Record = result?;
    //         // println!("{:?}", &record);
    //
    //         let entry = tracker.entry(record.0).or_insert(TemperatureTracker {
    //             min: i64::MAX as f64,
    //             max: i64::MIN as f64,
    //             sum: 0.0,
    //             count: 0,
    //         });
    //
    //         *entry = TemperatureTracker {
    //             min: record.1.min(entry.min),
    //             max: record.1.max(entry.max),
    //             sum: record.1 + entry.sum,
    //             count: entry.count + 1,
    //         };
    //
    //         n += 1;
    //
    //         if n % 1_000_000 == 0 {
    //             println!("Processed {} records", n);
    //         }
    //     }
    //
    //     for (key, value) in tracker.iter() {
    //         println!(
    //             "{}: min: {}, max: {}, avg: {}",
    //             key,
    //             value.min,
    //             value.max,
    //             value.sum / value.count as f64
    //         );
    //     }
    //
    //     Ok(())
}
