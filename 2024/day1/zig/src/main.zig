const std = @import("std");
const file_input = @embedFile("input.txt");

pub fn countLines(itr: std.mem.SplitIterator(u8, .any)) usize {
    var count: usize = 0;
    var it = itr;
    while (it.next()) |_| {
        count += 1;
    }

    return count;
}

pub fn parseInput(input: []const u8) !struct { []isize, []isize } {
    const line_count = countLines(std.mem.splitAny(u8, input, "\n")) - 1;

    var list1 = try std.heap.page_allocator.alloc(isize, line_count);
    var list2 = try std.heap.page_allocator.alloc(isize, line_count);

    var lines = std.mem.splitAny(u8, input, "\n");

    var idx: usize = 0;
    while (idx <= (line_count - 1)) {
        const line = lines.next().?;
        var tokens = std.mem.tokenizeAny(u8, line, "\t ");
        list1[idx] = try std.fmt.parseInt(isize, tokens.next().?, 10);
        list2[idx] = try std.fmt.parseInt(isize, tokens.next().?, 10);
        idx += 1;
    }

    return .{ list1, list2 };
}

pub fn compute_day1(lists: struct { []isize, []isize }) usize {
    std.mem.sort(isize, lists[0], {}, std.sort.asc(isize));
    std.mem.sort(isize, lists[1], {}, std.sort.asc(isize));

    //for (0..lists[0].len) |idx| {
    //    std.debug.print("{any}\t{any}\n", .{ lists[0][idx], lists[1][idx] });
    //}

    var total_dist: usize = 0;

    for (0..lists[0].len) |idx| {
        total_dist += @abs(lists[0][idx] - lists[1][idx]);
    }

    return total_dist;
}

pub fn compute_day2(lists: struct { []isize, []isize }) !isize {

    // Build a hashmap of value counts for list2
    var list2_vc = std.AutoHashMap(isize, isize).init(std.heap.page_allocator);

    for (lists[1]) |item| {
        try list2_vc.put(item, (list2_vc.get(item) orelse 0) + 1);
    }

    var similarity_score: isize = 0;

    for (lists[0]) |item| {
        similarity_score += (list2_vc.get(item) orelse 0) * item;
    }

    return similarity_score;
}

pub fn main() !void {
    const lists = try parseInput(file_input);
    //defer std.heap.page_allocator.free(lists.list1);
    //defer std.heap.page_allocator.free(lists.list1);
    const total_dist = compute_day1(lists);
    std.debug.print("Total Distance: {d}\n", .{total_dist});
    const similarity_score = try compute_day2(lists);
    std.debug.print("Similarity Score: {d}\n", .{similarity_score});
}
