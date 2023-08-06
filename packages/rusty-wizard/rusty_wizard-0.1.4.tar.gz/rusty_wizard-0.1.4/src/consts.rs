pub mod constants {
    pub const FAILED_PARSING_JSON_MESSAGE: &str = "Error: Could not parse JSON";

    pub const JSON_PICKLE_KEY_START : &str = "py/";

    pub const ALLOW_LIST_OBFUSCATION_JSONPICKLE_KEYS: [&str; 8] = [
        "py/iterator",
        "py/seq",
        "py/set",
        "py/tuple",
        "py/bytes",
        "py/b64",
        "py/b85",
        "py/property",
    ];

    pub const CENSORED_SIGN : &str = "*";

    pub const REGEX_DIVIDER: &str = "|";

    pub const NUMBER_OF_CENSORED_KEYS : usize = 45;

    pub const NULL_STRING: &str = "null";

    pub const GENERIC_DENY_LIST_KEYS: [&str; NUMBER_OF_CENSORED_KEYS] = [
        "api_?key",
        "auth_?key",
        "service_?key",
        "account_?key",
        "db_?key",
        "database_?key",
        "priv_?key",
        "private_?key",
        "client_?key",
        "db_?pass",
        "database_?pass",
        "key_?pass",
        "password",
        "passwd",
        "pwd",
        "secret",
        "jwt_?token",
        "access_?key",
        "access_?token",
        "smtp_?pass",
        "smtp_?pwd",
        "smtp_?user",
        "smtp_?user_?name",
        "admin_?pass",

        //AWS Environment Variables
        "aws_?access_?key",
        "aws_secret_access_key",
        "aws_session_token",
    
        "github_?token",
        "github_?client_?id",
        "github_?client_?secret",
        "github_?key",
        
        "client_?id",
        "client_?secret",
        "secret_?key",
    
        "azure_storage_?key",
        "azure_storage_?account",
        "azure_storage_connection_?string",
    
        "square_oauth_?secret",
        "square_oauth_?token",
    
        "ssh_private_?key",
        "ssh_private_key_?file",
        "ssh_public_?key",
        "ssh_public_key_?file",
        
        "gcloud_service_?key",
        "gcp_service_?key",
    ];

    pub type AdditionalLogicFunction = fn(&str, &str) -> bool;

}
