SELECT
    id,
	feature_image,
	title
FROM
	posts
WHERE
	feature_image IS NULL
	AND slug LIKE '%%roundup%%';