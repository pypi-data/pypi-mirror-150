var selected_data = {
    indexs: [],
    confidencs: [],
    variability: [],
    correctness: []
};
var inds = cb_obj.indices;
var d1 = s1.data;

for (var i = 0; i < inds.length; i++) {
    var idx = inds[i]
    selected_data["indexs"].push(idx)
    selected_data["confidencs"].push(d1["confidencs"][idx])
    selected_data["variability"].push(d1["variability"][idx])
    selected_data["correctness"].push(d1["correctness"][idx])
}

cs.data = selected_data;
cs.change.emit();