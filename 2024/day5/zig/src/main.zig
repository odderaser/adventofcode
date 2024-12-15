const std = @import("std");
const file_input = @embedFile("sample_input.txt");
const print = std.debug.print;
const parseInt = std.fmt.parseInt;

const Input = struct { rules: std.AutoArrayHashMap(usize, std.ArrayList(usize)), orderings: std.ArrayList([]const usize) };
const Rule = struct { before: usize, after: usize };

pub fn countSplitIterator(comptime T: type, itr: std.mem.SplitIterator(T, .any)) usize {
    var count: usize = 0;
    while (itr.next()) |_| {
        count += 1;
    }
    return count;
}

pub fn parseRule(input: []const u8) !?Rule {
    var rule_iterator = std.mem.splitAny(u8, input, "|");
    const key = try parseInt(usize, rule_iterator.next().?, 10);
    const value = try parseInt(usize, rule_iterator.next().?, 10);
    return Rule{ .before = key, .after = value };
}

pub fn parsePages(input: []const u8, allocator: *std.mem.Allocator) ![]const usize {
    const split_itr = std.mem.splitScalar(u8, input, ',');

    const page_nums = try allocator.alloc(usize, split_buffer.len);
    print("{d}\n", .{split_buffer.len});
    return page_nums;
}

pub fn parseInput(input: []const u8) !Input {
    var allocator = std.heap.page_allocator;
    var rules = std.AutoArrayHashMap(usize, std.ArrayList(usize)).init(allocator);
    var orderings = std.ArrayList([]const usize).init(allocator);

    var input_iterator = std.mem.splitAny(u8, input, "\n");

    var rule_mode: bool = true;
    //var ordering_idx: usize = 0;
    while (input_iterator.next()) |line| {
        print("{s}\n", .{line});
        if (line.len == 0) {
            // Assuming that the only empty line in the file splits rules and orderings
            print("Rule mode off!\n", .{});
            rule_mode = false;
        } else if (rule_mode) {
            const rule = (try parseRule(line)).?;
            const rule_array = try rules.getOrPut(rule.before);
            if (rule_array.found_existing) {
                try rule_array.value_ptr.append(rule.after);
            } else {
                var new_array = std.ArrayList(usize).init(allocator);
                try new_array.append(rule.after);
                rule_array.value_ptr.* = new_array;
            }
        } else {
            try orderings.append(try parsePages(line, &allocator));
        }
    }

    return Input{ .rules = rules, .orderings = orderings };
}

pub fn printAutoArrayHashMap(map: *std.AutoArrayHashMap(usize, std.ArrayList(usize))) void {
    var iter = map.iterator();

    while (iter.next()) |entry| {
        // Print the key
        const key = entry.key_ptr.*;
        std.debug.print("Key: {}\n", .{key});

        // Access the value (ArrayList) and print its contents
        const array_list = entry.value_ptr.*;
        std.debug.print("Values: ", .{});
        for (array_list.items) |item| {
            std.debug.print("{} ", .{item});
        }
        std.debug.print("\n", .{});
    }
}

pub fn main() !void {
    var parsed = try parseInput(file_input);
    print("{any}\n", .{parsed.rules});
    printAutoArrayHashMap(&parsed.rules);
}
