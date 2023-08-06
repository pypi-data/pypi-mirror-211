use regex::Regex;
use crate::plugins::jwt::jwt_plugin;
use crate::plugins::ssh::ssh_plugin;
use crate::plugins::github::github_plugin;
use crate::plugins::aws::aws_plugin;
use crate::consts::constants;
use crate::plugins::passwords::passwords_plugin;
use crate::plugins::azure::azure_plugin;
use crate::plugins::square_oauth::square_oauth_plugin;

pub struct Plugin {
    regex_for_value: Regex,
    additional_logic: Option<constants::AdditionalLogicFunction>
}

impl<'a> Plugin {
    pub fn new(regex_string: &'a str, additional_logic: Option<constants::AdditionalLogicFunction>) -> Self {
        Self {
            regex_for_value: Regex::new(regex_string).unwrap(),
            additional_logic,
        }
    }

    pub fn get_matched_strings(&self, json_value: &mut String) -> Vec<String> {
        let matched_strings = self.regex_for_value.find_iter(&json_value);
        let matched_string_vec: Vec<String> = matched_strings.map(|x| x.as_str().to_string()).collect();
        matched_string_vec
    }

    pub fn run(&self, key: &str, json_value: &mut String) -> bool {
        let mut did_replace = false;
        for regex_match in self.get_matched_strings(json_value) {
            match self.additional_logic {
                Some(additional_checks) => {
                    if (additional_checks)(key, &regex_match.as_str()) {
                        did_replace = true;
                        *json_value = json_value.replace(regex_match.as_str(), &constants::CENSORED_SIGN.repeat(regex_match.as_str().len()));
                    }
                }
                _ => {
                    did_replace = true;
                    *json_value = json_value.replace(regex_match.as_str(), &constants::CENSORED_SIGN.repeat(regex_match.as_str().len()));
                    }
            }
        }
        did_replace
    }
    
}

pub mod plugins_manager {
    use super::*;

    pub struct Manager {
        plugins: Vec<Plugin>,
        re: Regex
    }
    

    impl Manager {
        pub fn new() -> Self {
            Self {
                plugins: vec![
                    Plugin::new(jwt_plugin::JWT_TOKEN_REGEX, Some(jwt_plugin::jwt_checks)),
                    Plugin::new(ssh_plugin::SSH_PRIVATE_KEYS_REGEX, None),
                    Plugin::new(github_plugin::GITHUB_TOKEN_REGEX, None),

                    //AWS Plugins
                    Plugin::new(aws_plugin::AWS_ACCESS_KEY_REGEX, None),
                    Plugin::new(aws_plugin::AWS_AUTH_TOKEN_REGEX, None),

                    //Password Plugins
                    Plugin::new(passwords_plugin::PASSWORDS_REGEX, None),

                    // Azure Plugins
                    Plugin::new(azure_plugin::AZURE_STORAGE_KEY_REGEX, None),

                    // Square OAuth Plugins
                    Plugin::new(square_oauth_plugin::SQUARE_OAUTH_REGEX, None),

                ],
                re: Regex::new(&constants::GENERIC_DENY_LIST_KEYS.join(constants::REGEX_DIVIDER)).unwrap()
            }
        }
        pub fn run_plugins(&self, key: &str, json_string: &mut String, ignore_keys: bool) -> bool {
            let mut did_find_match_at_least_once = false;
            match ignore_keys {
                false => {
                    match self.re.is_match(&key.to_lowercase()) {
                        true => {
                            *json_string = constants::CENSORED_SIGN.repeat(json_string.len());
                            return true
                        }
                        false => {
                            for plugin in self.plugins.iter() {
                                let did_find_match = plugin.run(key, json_string);
                                match did_find_match {
                                    true => {
                                        did_find_match_at_least_once = true;
                                    },
                                    false => ()
                                }
                            }
                        }
                    }
                },
                true => ()
            }
            did_find_match_at_least_once
        }

    }
}
