pub mod ssh_plugin {
    pub const SSH_PRIVATE_KEYS_REGEX: &str = r".*[\-]{3,}BEGIN (RSA|DSA|EC|OPENSSH|PGP|PRIVATE)? ?(PRIVATE)? KEY[\-]{3,}(.|\n){0,150}";
}
