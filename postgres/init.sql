CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL DEFAULT 'https://res.cloudinary.com/dkezdazmt/image/upload/v1742874598/MiniProject/profile.svg'
);


CREATE TABLE IF NOT EXISTS THREATS (
    id SERIAL PRIMARY KEY,
    threat_id INT NOT NULL,
    name VARCHAR(32) NOT NULL,
    ip VARCHAR(32) NOT NULL,
    timestamp VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS SUGGESTIONS (
    suggestion varchar(255) NOT NULL,
    threat_id INT NOT NULL
);


INSERT INTO SUGGESTIONS (suggestion, threat_id) VALUES
('Use parameterized queries or prepared statements in all SQL interactions.', 1),
('Apply input validation and sanitization on all user inputs.', 1),
('Implement ORM frameworks to abstract direct SQL usage.', 1),
('Avoid concatenating SQL queries with untrusted data.', 1),
('Enforce least privilege on database accounts used by the app.', 1),
('Monitor and log abnormal query patterns in real-time.', 1),
('Employ Web Application Firewalls (WAF) to filter malicious requests.', 1);


INSERT INTO SUGGESTIONS (suggestion, threat_id) VALUES
('Implement rate limiting and account lockout policies.', 2),
('Use CAPTCHA to prevent automated login attempts.', 2),
('Enforce strong password complexity rules.', 2),
('Enable multi-factor authentication (MFA) for user accounts.', 2),
('Monitor login attempts and set up alerting for anomalies.', 2),
('Log and analyze failed login attempts for suspicious patterns.', 2),
('Apply exponential backoff delays on failed logins.', 2);
