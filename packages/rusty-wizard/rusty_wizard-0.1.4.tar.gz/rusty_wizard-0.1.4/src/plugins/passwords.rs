pub mod passwords_plugin {
    pub const PASSWORDS_REGEX: &str = r#"(db_?pass|database_?pass|key_?pass|password|passwd|pwd)(\\|"| )*:("|\\| )*([a-z]|[A-Z]|[0-9]|@|#|\$|%|\^|&|\+|\*|=|!){8,36}("|}|\\){0,1}"#;
}
