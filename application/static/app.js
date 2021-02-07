//Searches for books based on title and loads them to the screen.
async function search_book(searchterm){
    url = 'https://www.googleapis.com/books/v1/volumes?q=';
    resp = await axios.get(`${url}${searchterm}`);
    data = resp.data.items;
    username = $("#user").text();
    res = await axios.get(`/users/search/${username}`);
    $user = res.data;
    $row = $("#top_book_row");
    $row.empty();
    for(let point in data){
        img = data[point]['volumeInfo']['imageLinks']['thumbnail'];
        title = data[point]['volumeInfo']['title'];
        book_card = `<div class="col-2 my-2 mx-2 text-center">
                        <div class="row mx-auto">
                            <img src="${img}" alt="${title}" class="img-fluid rounded">
                        </div
                        <div class="row text-center">
                            <h5>${title}</h5>
                            <a href="/users/${$user}/library/check/${title}" class="btn btn-success my-1">Add to Library</a>
                            <a href="/books/check/${title}" class="btn btn-primary my-1">View Details</a>
                        </div>
                    </div>`;
        $row.append(book_card);
    }
}
function open_comment(e){
    e.preventDefault();
    $form = $("#comment-form")
    $("#reply").addClass("disabled");
    $form.removeClass("invisible");
}
function book_search(e){
    e.preventDefault();
    $search_term = $("#search_bar").val();
    search_book($search_term);
}
$('#search').on("click", book_search);
$("#reply").on("click", open_comment);