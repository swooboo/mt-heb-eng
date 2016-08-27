# Web server deployment instructions

The front end of the project is a Flask-based web service, written in Python. This document describes the web server deployment process.

### Prequisites:

* A Linux server on which the server will run. Should be exposed to the Internet, with the ability to open ports
	* If the server is not exposed, but connected to the internet, there is a way to tunnel the ports with SSH.
* Flask web server installed on the aforementioned server
* The source code of the service [here](https://github.com/swooboo/mt-heb-eng.git):
* Translation model trained by moses, [instructions](https://github.com/swooboo/mt-heb-eng/blob/master/docs/training_instructions.md)
* Patience

### Working plan:

1. Get the source code
2. Apply the configurations
3. Run the server
4. Set up Putty tunneling of the needed ports
5. (Optional) Set up SSH tunneling, in case the server is not exposed

### Get the source code and apply configurations

* Clone from Git:
	
	```bash
	git clone https://github.com/swooboo/mt-heb-eng.git
	cd mt-heb-eng
	```
* Check the configuration file, defaults should be fine:

	```
	$ cat ./moses.config.json
	{
			"name": "moses",
			"host": "http://localhost:8080/RPC2",
			"start_cmd": "( ~/mosesdecoder/bin/moses -f ~/working/binarised-model/moses.ini --daemon --server --server-log ~/moses.log 2>>~/moses.log & )",
			"check_cmd": "pidof moses",

			"tokenize_cmd": "~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en"
	}
	```

### Run the server

* We're running a [Flask](http://flask.pocoo.org/) server
* To run:

	```
	$ ./webserver.py
	 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	 * Restarting with stat
	 * Debugger is active!
	 * Debugger pin code: 142-822-366
	```
	* Note that the web server listens to port `5000`, the port should be available
	* The pin code is for debugging. For example, http://127.0.0.1:5000/tr throws an exception and can be debugged live
* The server will try to run Moses when a translation is queried, be sure Moses is well-trained and can be run in daemon-server mode. If any problems arise, try to run `start_cmd` from the `moses.config.json` manually to see the output, and note where the logs are written to.

### Set up Putty tunneling of the needed ports

In case the server is not exposed, and there is a need to make the service available to the Internet, we'll need some tricky SSH tunneling to be set up. Take a look at the configuration this project deployment needed to work with:

**University Server - `S1`** <--> **Service Server - `S2` (*has Internet access to outside, but not directly from outside*)**

The Univerity server (`S1`) can be accessed directly from the Internet, but ports can not be opened on it to be available outside, as it was behind a firewall. S2 can also not open any ports to outside (only locally), but has Internet access. To access `S2` and deploy the server, we needed to initially access `S1`, then SSH to `S2`. [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) was used like this:

1. Run Putty
2. Set up a port forwarding with rule `L80	localhost:5000`
	* This means that on the client machine (laptop), port 80 will be forwarded to the server machine (`S1`) port 5000.
3. Tunnel port 5000 from `S2` to `S1`:

	```bash
	ssh -R :5000:localhost:5000 S1
	```
	* Note that this needs to be run from `S2`. A shell will be opened on `S1`, and that shell needs to stay opened.
4. Now, ports are forwarded as follows:
	* **laptop:80** <--> **S1:5000** <--> **S2:5000**
5. As a result, surfing to http://127.0.0.1 gives the same result as if we surfed from `S2` to http://127.0.0.1:5000
6. The problem with this setup is that the service is not accessible to the Internet, only to the `localhost` of the computer (the laptop in this case) that's connecting to the server.
	* In order to make it accessible to the Internet, either the laptop should be exposed to the Internet, or another workstation that we have full control over needs to be configured to be accessible correctly from the outside. Check the next section for this solution.

### (Optional) Set up SSH tunneling, in case the server is not exposed

This section is a tutorial on how to make the service fully accessible to the Internet. The end result is the surfing to a domain http://tr.swooboo.com from **any** client would be the same as surfing to http://127.0.0.1:5000 from `S2`. We achieve this by setting up the following server configuration:

**S1** <--> **S2** <--> **Owned server - S3** <--> Internet

Or, if `S3` is behind a router:

**S1** <--> **S2** <--> **Owned server - S3** <--> **Router - R1** <--> Internet

Note that `S1` <--> `S2` is not important here, we only need it to access `S2`.

Our game plan:

1. Tie `S3` to a domain name using Dynamic DNS (we'll use http://tr.swooboo.com for this example)
2. Configure SSH daemon of `S3` to accept inbound tunneling of port `5000` (off by default)
	* The tunnel should also open the port `5000` to the outside of `S3`, not only locally
3. Configure the router to forward all connections to `S3` - set it to DMZ
4. Set up port forwarding of port `80` of the router to `S3:5000`
5. Set up SSH keys to be able to passwordlessly connect from `S2` to `S3`
5. Tunnel `S2:5000` to `S3:5000`
6. Enjoy the web service exposed at http://tr.swooboo.com

#### 1. Tie `S3` to a domain name using Dynamic DNS

1. Register at http://internetbs.com
2. Buy a domain, for our example I already had the domain http://swooboo.com
3. Log in to Internet.bs and surf to the domain page
4. Surf to 'DNS Management' ([link](https://internetbs.net/en/domain-name-registrations/controller.html?action=DNSManagementAction&clickIdTrack=2c1133138b86168daec905e2ed87aac2&manageDomainsViewMode=2&isJavascriptEnabled=1&reqkey=6ddc2509adb9be679e3219d0c6540dcd9c1f2bd4), hopefully it will work)
5. Add the following entry to 'Dynamic DNS Records' (replace the <> values with custom ones):
	* tr.swooboo.com | 60 | <empty 'Offline Address'> | <username> | <password>
	* Note: username and password are irrelevant, they just need to be remembered for a couple of minutes
6. Click on 'Apply' - floppy disk icon near our newly added entry
7. Add a cron in `S3`:

```bash
crontab -e
```
8. The following cron should be added:

	```
	*/5 * * * * ( date ;curl 'https://dyndns.topdns.com/update?hostname=tr.swooboo.com&username=<username>&password=<password>' ;echo ) >> /tmp/dyndns.log
	```
	* Replace the <> values with the username and the password that were set in the Dynamic DNS entry
	* This will make `S3` fire the `dyndns` URL every 5 minutes. Every time the URL is fired, Internet.bs will update the http://tr.swooboo.com domain address with the IP of `S3`, so if the IP changes, it will take up to 5 minutes for it tu update.
9. Now, if the domain is pinged - `ping tr.swooboo.com`, the IP will be that of `S3` regardless of IP change
