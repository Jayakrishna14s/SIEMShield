use std::net::ToSocketAddrs;

fn main() {
    let domains = vec![
        "google.com",
        "example.com",
        "rust-lang.org",
        "openai.com",
        "nonexistentdomain.abc",
    ];

    for domain in domains {
        let address = format!("{}:80", domain); // Add port to satisfy ToSocketAddrs

        println!("\n📦 Domain: {}", domain);
        match address.to_socket_addrs() {
            Ok(iter) => {
                let mut found = false;
                for ip in iter {
                    println!("  ➤ IP: {}", ip.ip());
                    found = true;
                }
                if !found {
                    println!("  ⚠️ No IPs found");
                }
            }
            Err(e) => {
                println!("❌ Failed to resolve {}: {}", domain, e);
            }
        }
    }
}
