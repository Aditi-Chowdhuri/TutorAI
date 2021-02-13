def read_data(fb):
    data=fb.get("/", "courses")
    cname_arr = data.keys()
    cname_arr=sorted(cname_arr, reverse=True, key=lambda x: data[x]['views'])
    return cname_arr, data
