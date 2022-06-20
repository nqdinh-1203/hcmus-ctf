## HCMUS-CTF 2022: Challenge name

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-Emon-blue.svg)  
![solves](https://img.shields.io/badge/Solves-16-lightgrey.svg)

### Description
- forgot

### Hints
- None

### Attached files
- Lost

### Summary
- We can register existing account and easy login as `admin_1, admin_2, ...`
- Because the challange does not verify the token, another way to login to abitrary account is to change the jwt token
- The signature is create using the fomular `HMAC(username + key)`, therefor we can easy recover the signature. For example `username = 'admin_1k'` and `key = 'ey'`

### Detailed solution
First, register `admin_1k` account
```
POST http://103.245.250.31:32322/auth/register
{
    "uname": "admin_3k",
    "pwd": "0000"
}
```
![step 1](step1.png)

Second, login as that user and got the token
```
POST http://103.245.250.31:32322/auth/login
{
    "uname": "admin_3k",
    "pwd": "0000"
}
```
![step 2](step2.png)

Third, set that token to header and insert data with key `ey` get signature
```
POST http://103.245.250.31:32322/api/insert-data
{
    "key": "ey",
    "data": "so lucky"
}
```
![step 3](step3.png)

Fourth, create `admin_1` token either by register existing accout or fake jwt. We will get some thing like:
> token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmFtZSI6ImFkbWluXzEiLCJleHAiOjE2NTI3NTU3MjN9.EaJWw-qrgT8nDSfjiy1m04d3fcZY8nFjMgFnq7EGZf4; Expires=Tue, 17 May 2022 02:48:43 GMT

Fifth, set admin token and signature to header, and get data `key`
```
POST http://103.245.250.31:32322/api/data
{
    "key": "key"
}
```
![step 5](step5.png)

### Flag
```
HCMUS-CTF{Y_U_DoNt_H4ve_Fr0nt_3nddd????}
```
