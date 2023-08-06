mod plugins;
mod consts;
mod manager;

use std::ptr;
use std::string::String;

use pyo3::types::PyString;
use pyo3::prelude::*;
use serde_json::Value;

use manager::plugins_manager::Manager;
use consts::constants;

static mut PLUGINS_MANAGER: *mut Manager = ptr::null_mut();

#[pyfunction]
fn replace_secrets_in_json(json_to_check: &PyString) -> &PyString {
    let mut rust_string = json_to_check.to_string();
    if rust_string == constants::NULL_STRING {
        return json_to_check;
    }
    let json_value = use_extract_strings(&mut rust_string);
    if json_value.is_null() {
        return PyString::new(json_to_check.py(), constants::FAILED_PARSING_JSON_MESSAGE);
    }
    PyString::new(json_to_check.py(), &json_value.to_string())
}

#[pymodule]
fn rusty_wizard(_py: Python, module: &PyModule) -> PyResult<()> {
    let manager = Manager::new();
    unsafe {
        PLUGINS_MANAGER = Box::into_raw(Box::new(manager));
    }
    module.add_function(wrap_pyfunction!(replace_secrets_in_json, module)?)?;
    Ok(())
}

fn is_jsonpickle_key(key: &str) -> bool {
    key.starts_with(constants::JSON_PICKLE_KEY_START)
}

fn should_skip_obfuscation(key: &str) -> bool {
    is_jsonpickle_key(key) && !constants::ALLOW_LIST_OBFUSCATION_JSONPICKLE_KEYS.contains(&key)
}

fn extract_strings(json: &mut Value, relevant_key: &str, real_key: &str) {
    match json {
        Value::String(string_value) => {
            if should_skip_obfuscation(real_key) {
                return;
            }
            unsafe {
                (*PLUGINS_MANAGER).run_plugins(relevant_key, string_value, false);
            }
        },
        Value::Array(list) => {
            for (_index, value) in list.iter_mut().enumerate() {
                extract_strings(value, relevant_key, real_key);
            }
        },
        Value::Object(map) => {
            for (object_key, object_value) in map {
                extract_strings(object_value, if is_jsonpickle_key(object_key) {&relevant_key} else {&object_key}, &object_key);
            }
        }
        // Those three are to cover all of the different cases, but we don't need to do anything (more clear thaj using _ => ())
        Value::Number(_number_value) => (),
        Value::Bool(_bool_value) => (),
        Value::Null => (),
        }
}

fn use_extract_strings(json_string: &mut String) -> Value {
    let mut json: Value = match serde_json::from_str::<Value>(json_string) {
        Ok(value) => value,
        Err(_) => return Value::Null
    };
    extract_strings(&mut json, "", "");
    json
}
