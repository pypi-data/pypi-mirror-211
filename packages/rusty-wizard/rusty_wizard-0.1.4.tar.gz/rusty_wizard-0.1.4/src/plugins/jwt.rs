pub mod jwt_plugin {
    pub const JWT_TOKEN_REGEX: &str = r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*?";

    const BASE64_VALID_DIVIDER: usize = 4;
    const LAST_PART_INDEX: usize = 2;

    pub fn jwt_checks(_key: &str, token: &str) -> bool {
        let parts = token.split(".");
        for (index, part_str) in parts.enumerate() {
            let base64_remainder = part_str.len() % BASE64_VALID_DIVIDER;
            let part = match base64_remainder {
                1 => return false,
                2 => format!("{}{}", part_str, "=="),
                3 => format!("{}{}", part_str, "="),
                _ => part_str.to_string()
            };
            match base64::decode_config(part, base64::URL_SAFE) {
                Ok(b64_decoded) => {
                    if index < LAST_PART_INDEX {
                        let payload_str = match String::from_utf8(b64_decoded) {
                            Ok(base64_decoded_string) => base64_decoded_string,
                            Err(_) => return false,
                        };
                        match serde_json::from_str::<serde_json::Value>(&payload_str) {
                            Ok(_) => (),
                            Err(_) => return false,
                        }
                    }
                }
                Err(_) => return false,
            }
        }
        true
    }
}
