import requests
import hashlib
import sys 

#requests pw data and gives us response
def request_api_data(query_char):
	url = "https://api.pwnedpasswords.com/range/" + query_char
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f"Error fetching: {res.status_code}, check the API and try again")
	return res


#shows how many times certain password has been leaked
def get_password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(":") for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == hash_to_check:
			return count 
	return 0 

#check if pw is in api
def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
	first5_char,tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	return get_password_leaks_count(response, tail)

#arugments and fstrings!!!
def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f"{password} was found {count} times... GO CHANGE YOUR PASSWORD!")
		else:
		 	print(f"{password} was NOT found. ALL GOOD!")
		return "done!!"




if __name__== "__main__":
	sys.exit(main(sys.argv[1:]))