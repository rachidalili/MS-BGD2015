from github3 import login

gh = login('chkhalil', password='bismallahazerty123A')

ch_user = gh.user()
# <User [ch_user:Ian Cordasco]>

print(ch_user.name)
# Ian Cordasco
print(ch_user.login)
# ch_user
print(ch_user.followers)
# 4

#for f in gh.iter_followers():
 #   print(str(f))

kennethreitz = gh.user('Ocramius')
# <User [kennethreitz:Kenneth Reitz]>

print(kennethreitz.name)
print(kennethreitz.login)
print(kennethreitz.followers)
#print(kennethreitz.iter_repos)
#followers = [str(f) for f in gh.iter_followers('kennethreitz')]
gh.user('Ocramius')
repos = [r.refresh() for r in gh.iter_repos('kennethreitz')]
print repos
