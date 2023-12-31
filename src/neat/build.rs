use std::env;
use std::path::{Path};

fn main() {
    let pwd_dir = env::var("CARGO_MANIFEST_DIR").unwrap();
    let path = Path::new(&*pwd_dir).join("dep");
    println!("cargo:rustc-link-search=native={}", path.to_str().unwrap());
    println!("cargo:rustc-link-lib=dylib=feedforward");
    // println!("cargo:rustc-link-lib=static=add");
    // println!("cargo:rerun-if-changed=src/hello.c");
}

