SELECT
	id
FROM
	posts
WHERE
	html NOT LIKE '%%alt%%'
	AND html LIKE '%%img%%'
	AND html LIKE '%%kg-image-card%%'
	AND status = 'published';