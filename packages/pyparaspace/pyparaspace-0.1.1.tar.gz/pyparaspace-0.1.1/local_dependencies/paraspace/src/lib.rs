pub mod problem;
pub mod tokensolver;
mod multiplicity;
pub mod transitionsolver;
pub mod cores;
// mod cores;

pub fn solve_json(input :String) -> String {
    let problem = serde_json::de::from_str::<problem::Problem>(&input).unwrap();
    println!("{:#?}", problem);
    "".to_string()
}

pub fn print_calc_time<T>(name: &str, f: impl FnOnce() -> T) -> T{
    use std::time::Instant;
    let now = Instant::now();

    let result = {
        f()
    };

    let elapsed = now.elapsed();
    println!("{} took {:.2?}", name, elapsed);
    result
}

#[derive(Clone, Debug)]
pub enum SolverError {
    NoSolution,
    GoalValueDurationLimit,
    GoalStateMissing,
}


pub fn from_z3_real(real: &z3::ast::Real) -> f32 {
    let (num, den) = real.as_real().unwrap();
    num as f32 / den as f32
}
