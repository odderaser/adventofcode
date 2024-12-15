const std = @import("std");
const file_input = @embedFile("input.txt");

pub fn countTokens(comptime T: type, itr: std.mem.TokenIterator(T, .scalar)) usize {
    var count: usize = 0;
    var it = itr;
    while (it.next()) |_| {
        count += 1;
    }
    return count;
}

pub fn parseInput(input: []const u8) !std.ArrayList([]const isize) {
    const allocator = std.heap.page_allocator;

    var output = std.ArrayList([]const isize).init(allocator);
    var reports = std.mem.splitAny(u8, input, "\n");

    while (reports.next()) |report| {
        const num_levels = countTokens(u8, std.mem.tokenizeScalar(u8, report, ' '));
        if (num_levels > 0) {
            var levels_arr = try allocator.alloc(isize, num_levels);
            var level_tokens = std.mem.tokenizeScalar(u8, report, ' ');
            var idx: usize = 0;
            while (level_tokens.next()) |level| {
                levels_arr[idx] = try std.fmt.parseInt(isize, level, 10);
                idx += 1;
            }
            try output.append(levels_arr);
        }
    }

    return output;
}

pub fn sumBool(bool_arr: []bool) usize {
    var result: usize = 0;
    for (bool_arr) |b| {
        if (b) {
            result += 1;
        }
    }
    return result;
}

pub fn checkReportSafety(report: []const isize, dampener: bool) !bool {
    const allocator = std.heap.page_allocator;

    var diff_arr = try allocator.alloc(isize, report.len - 1);
    var diff_sign_sum: isize = 0;

    for (0..(report.len - 1)) |idx| {
        diff_arr[idx] = report[idx + 1] - report[idx];
        diff_sign_sum += std.math.sign(diff_arr[idx]);
    }

    var abs_mask = try allocator.alloc(bool, diff_arr.len);
    var sign_mask = try allocator.alloc(bool, diff_arr.len);
    var combined_mask = try allocator.alloc(bool, diff_arr.len);

    for (0..diff_arr.len) |idx| {
        abs_mask[idx] = 0 < @abs(diff_arr[idx]) and @abs(diff_arr[idx]) <= 3;
        sign_mask[idx] = std.math.sign(diff_arr[idx]) == std.math.sign(diff_sign_sum);
        combined_mask[idx] = abs_mask[idx] and sign_mask[idx];
    }

    if (std.mem.allEqual(bool, combined_mask, true)) {
        return true;
    } else if (dampener) {
        for (0..report.len) |idx_rm| {
            const idx_rm_report = try allocator.alloc(isize, report.len - 1);
            defer allocator.free(idx_rm_report);

            var offset: usize = 0;

            for (0..(report.len - 1)) |idx| {
                if (idx == idx_rm) {
                    offset += 1;
                }
                idx_rm_report[idx] = report[idx + offset];
            }

            if (try checkReportSafety(idx_rm_report, false)) {
                return true;
            }
        }
        return false;
    } else {
        return false;
    }
}

pub fn main() !void {
    const reports = try parseInput(file_input);
    var num_safe_reports: usize = 0;
    var num_safe_reports_w_dampener: usize = 0;

    for (reports.items) |report| {
        if (try checkReportSafety(report, false)) {
            num_safe_reports += 1;
        }
    }

    std.debug.print("Number of safe reports: {d}\n", .{num_safe_reports});

    for (reports.items) |report| {
        if (try checkReportSafety(report, true)) {
            num_safe_reports_w_dampener += 1;
        }
    }

    std.debug.print("Number of safe reports w/ dampener: {d}\n", .{num_safe_reports_w_dampener});
}
