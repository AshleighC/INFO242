import sys
from bs4 import BeautifulSoup
from converter import pretty_print, print_simple

def print_event_actor(actor, indent, spaces):
  pretty_print('<actor type="%s">' % actor.type.string, indent)
  print_simple('login', actor.login.string, indent + spaces)
  if actor.find('name'):
    print_simple('name', actor.find('name').string, indent + spaces)
  if actor.email:
    print_simple('email', actor.email.string, indent + spaces)
  if actor.location:
    print_simple('location', actor.location.string, indent + spaces)
  if actor.blog:
    print_simple('blog', actor.blog.string, indent + spaces)
  pretty_print('</actor>', indent)

def print_event(event, indent, spaces):
  print_simple('date', event.find('created_at', recursive=False).string, indent)
  print_event_actor(event.find('actor_attributes'), indent, spaces)

def print_events(events, indent, spaces):
  pretty_print('<events>', indent)
  for event in events:
    if event.repository:
      pretty_print('<event type="%s" repoID="%s">' % (event.find('type', recursive=False).string, event.repository.id.string), indent + spaces)
      print_event(event, indent + (2 * spaces), spaces)
      pretty_print('</event>', indent + spaces)
  pretty_print('</events>', indent)

def print_repo_basics(repo, indent, spaces):
  print_simple('name', repo.find('name').string, indent)
  print_simple('owner', repo.find('owner').string, indent)
  if repo.find('description'):
    print_simple('description', repo.find('description').string, indent)

def print_repo_dates(repo, indent, spaces):
  pretty_print('<dates>', indent)
  print_simple('date', repo.created_at.string, indent + spaces, {'of': 'creation'})
  print_simple('date', repo.pushed_at.string, indent + spaces, {'of': 'push'})
  pretty_print('</dates>', indent)

def print_repo_urls(repo, indent, spaces):
  pretty_print('<urls>', indent)
  print_simple('url', repo.url.string, indent + spaces, {'of': 'github'})
  if repo.homepage:
    print_simple('url', repo.homepage.string, indent + spaces, {'of': 'homepage'})
  if repo.has_wiki.string != 'False':
    print_simple('url', repo.url.string + '/wiki', indent + spaces, {'of': 'wiki'})
  pretty_print('</urls>', indent)

def print_repo_languages(repo, indent, spaces):
  pretty_print('<languages>', indent)
  if repo.language:
    print_simple('language', repo.language.string, indent + spaces)
  pretty_print('</languages>', indent)

def print_repo_metrics(repo, indent, spaces):
  pretty_print('<metrics>', indent)
  pretty_print('<metric type="size">', indent + spaces)
  print_simple('value', repo.size.string, indent + (2 * spaces))
  print_simple('unit', 'bytes', indent + (2 * spaces))
  pretty_print('</metric>', indent + spaces)
  pretty_print('<metric type="network">', indent + spaces)
  print_simple('relation', repo.watchers.string, indent + (2 * spaces), {'description': 'watchers'})
  print_simple('relation', repo.forks.string, indent + (2 * spaces), {'description': 'forks'})
  print_simple('relation', repo.open_issues.string, indent + (2 * spaces), {'description': 'issues'})
  pretty_print('</metric>', indent + spaces)
  pretty_print('</metrics>', indent)

def print_repo(repo, indent, spaces):
  print_repo_basics(repo, indent, spaces)
  print_repo_dates(repo, indent, spaces)
  print_repo_urls(repo, indent, spaces)
  print_repo_languages(repo, indent, spaces)
  print_repo_metrics(repo, indent, spaces)

def print_repos(repos, indent, spaces):
  repo_ids = []
  pretty_print('<repositories>', indent)
  for repo in repos:
    repo_id = repo.id.string
    if repo_id not in repo_ids:
      repo_ids.append(repo_id)
      pretty_print('<repository id="%s" fork="%s">' % (repo_id, repo.fork.string), indent + spaces)
      print_repo(repo, indent + (2 * spaces), spaces)
      pretty_print('</repository>', indent + spaces)
  pretty_print('</repositories>', indent)

if (__name__ == '__main__') and (len(sys.argv) == 2):
  f = open(sys.argv[1])
  soup = BeautifulSoup(f.read(), 'xml')
  f.close()
  indent, spaces = 0, 2
  pretty_print('<?xml version="1.0" encoding="UTF-8"?>', indent)
  pretty_print('<github_data>', indent)
  print_events(soup.find_all('event'), indent + spaces, spaces)
  print_repos(soup.find_all('repository'), indent + spaces, spaces)
  pretty_print('</github_data>', indent)

