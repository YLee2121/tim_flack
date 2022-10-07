function deleteNote(product_id) {
    fetch('/profile/delete/', {
      method: "POST",
      body: JSON.stringify({ product_id: product_id }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }