flake8:
	flake8 --append-config roundup/.flake8 --count --max-complexity=10 --max-line-length=120 --statistics roundup

bandit:
	bandit --baseline .bandit_baseline.json -ll -s B101,B103,B608 -f custom --msg-template "{relpath}:{line}: {test_id}[bandit]: {severity}: {msg}" -r roundup

bandit_boostrap:
