pub mod aws_plugin {
    pub const AWS_ACCESS_KEY_REGEX: &str = r"AKIA[0-9A-Z]{16}";
    pub const AWS_AUTH_TOKEN_REGEX: &str = r"amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}";
}
