import pandas


def get_genre_with_count(conn):
    sql_query = '''
        SELECT genre_id, genre_name, COUNT(book_id) as book_count
        FROM book JOIN genre USING(genre_id)
        GROUP BY genre_id
        ORDER BY 2;
    '''

    return pandas.read_sql(sql_query, conn)


def get_author_with_count(conn):
    sql_query = '''
        SELECT author_id, author_name, COUNT(book_id) as book_count
        FROM book_author JOIN author USING(author_id)
        GROUP BY author_name
        ORDER BY 2;
    '''

    return pandas.read_sql(sql_query, conn)


def get_publisher_with_count(conn):
    sql_query = '''
        SELECT publisher_id, publisher_name, COUNT(book_id) as book_count
        FROM book JOIN publisher USING(publisher_id)
        GROUP BY publisher_id
        ORDER BY 2;
    '''

    return pandas.read_sql(sql_query, conn)


def get_filtered_books(conn, genres, authors, publishers):
    sql_query = f'''
        WITH get_authors(book_id, authors_name)
                 AS (SELECT book_id, GROUP_CONCAT(author_name, ', ')
                     FROM author
                              JOIN book_author USING (author_id)
                     GROUP BY book_id)
        SELECT DISTINCT book_id, title, authors_name, genre_name, publisher_name, year_publication, available_numbers
        FROM book
                 JOIN get_authors USING (book_id)
                 JOIN book_author USING (book_id)
                 JOIN author USING (author_id)
                 JOIN publisher USING (publisher_id)
                 JOIN genre USING (genre_id)
        WHERE TRUE
            -- {'TRUE' if len(genres) == 0 and len(authors) == 0 and len(publishers) == 0 else 'FALSE'}
            {'AND book.genre_id IN (' + ', '.join(genres) + ')' if len(genres) > 0 else ''}
            {'AND author_id IN (' + ', '.join(authors) + ')' if len(authors) > 0 else ''}
            {'AND book.publisher_id IN (' + ', '.join(publishers) + ')' if len(publishers) > 0 else ''}
        ORDER BY 2
    '''

    return pandas.read_sql(sql_query, conn)
