const onDelete = (_, url) => {
  if (!url) return;
  fetch(url, { method: "delete" }).then((res) => {
    if (res.ok) {
      window.location.reload();
    } else {
      alert("error deleting resource");
    }
  });
};
