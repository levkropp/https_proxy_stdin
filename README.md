# https_proxy_stdin
<p align="center">
  <img src="https://i.imgur.com/P1zzEJl.png">
</p>

Welcome to our repository! 🎉 Here you can find a pair of scripts designed to check the availability of a list of HTTPS proxies. The purpose of these scripts is to provide a secure and private way to check the validity of proxies without exposing them to potential exposure or theft by online proxy checking services. When you use online services to check your proxies, they often add your proxies to their free proxy lists, making them public, which is not desirable for your privacy and the longevity of the proxy.

## 📁 Files

### `format_proxies.sh` 🖥️

This is a Bash script that formats a list of proxies for use with the Python 🐍 script. It reads from the standard input, trims whitespace, removes invalid lines, and converts each proxy to a Python string. The output is a Python list of strings, printed to the standard output.

This script should be used to format a list of proxies before it is passed to the Python script. For example:

```bash
cat proxies.txt | ./format_proxies.sh | python check_proxies.py
```

### `check_proxies.py` 🕵️‍♀️

This is a Python script that checks a list of proxies to see if they are available. The list of proxies is read from the standard input. It uses multithreading to speed up the process 🚀.

The script accepts a `-t` argument which specifies the number of threads to use. For example:

```bash
python check_proxies.py -t 32
```

This will use 32 threads to check the proxies. If the `-t` argument is not provided, the script will default to using 16 threads.

Each proxy is checked by attempting to make a GET request to a URL. If the request is successful, the proxy is considered valid ✔️.

## 👨‍💻 Usage

To use these scripts together, you can use a command like the following:

```bash
cat proxies.txt | ./format_proxies.sh | python check_proxies.py -t 32
```

This command will read a list of proxies from `proxies.txt`, format them using `format_proxies.sh`, and then check each proxy using `check_proxies.py` with 32 threads. The results will be printed to the console. This process ensures that your proxies remain private and are not shared with any third-party service, ensuring their longevity and your privacy 🕶️.

# 📝 TODO

1. **Add URL parameter to Python script:** 🎯 Implement a command-line option for the Python script (`check_proxies.py`) that allows the user to set the URL that will be used for proxy checking.

2. **Enhance error handling:** 🚧 Improve the error handling in both scripts to provide more detailed feedback to the user when something goes wrong, such as when the input format is incorrect or the specified URL is not reachable.

3. **Support for proxy authentication:** 🔐 Update the Python script to support proxies that require username/password authentication.

4. **Performance optimization:** ⚡ Investigate ways to optimize the performance of the scripts, such as by improving the multithreading in the Python script or streamlining the text processing in the Bash script.
