const std = @import("std");
const input_file = @embedFile("input.txt");
const print = std.debug.print;

const AnsiColor = enum {
    Red,
    Green,
    Blue,
    Reset,
};

fn getAnsiCode(color: AnsiColor) []const u8 {
    return switch (color) {
        .Red => "\x1b[31m",
        .Green => "\x1b[32m",
        .Blue => "\x1b[34m",
        .Reset => "\x1b[0m",
    };
}

pub fn printc(comptime fmt_string: []const u8, color: AnsiColor, args: anytype) void {
    const color_code = getAnsiCode(color);
    const reset_code = getAnsiCode(AnsiColor.Reset);

    std.debug.print("{s}", .{color_code});
    std.debug.print(fmt_string, args);
    std.debug.print("{s}", .{reset_code});
}

const Bounds = struct { start: usize, end: usize };

const ExprBounds = struct {
    start: usize,
    end: usize,
    arg_bounds: []Bounds,
};

pub fn findExpr(comptime prefix: []const u8, comptime suffix: []const u8, comptime nargs: usize, input: []const u8) ?ExprBounds {
    // This implementation assumes that the arg types are integers
    var idx: usize = 0;
    var arg_bounds: [nargs]Bounds = undefined;

    while (idx < input.len) {
        if (std.mem.startsWith(u8, input[idx..], prefix)) {
            const start = idx;
            idx += prefix.len;

            var args_parsed: usize = 0;
            var arg_start_idx: usize = idx;
            while (args_parsed < nargs) {
                if (std.ascii.isDigit(input[idx])) {
                    idx += 1;
                } else if ((input[idx] == ',' or std.mem.endsWith(u8, input[idx..(idx + suffix.len)], suffix)) and idx > arg_start_idx) {
                    arg_bounds[args_parsed] = Bounds{ .start = arg_start_idx, .end = idx };

                    if (input[idx] == ',') {
                        idx += 1;
                    } else if (std.mem.endsWith(u8, input[idx..(idx + suffix.len)], suffix)) {
                        idx += suffix.len;
                        return .{ .start = start, .end = idx, .arg_bounds = &arg_bounds };
                    }

                    args_parsed += 1;
                    arg_start_idx = idx;
                } else {
                    break;
                }
            }

            if (std.mem.endsWith(u8, input[idx..(idx + suffix.len)], suffix)) {
                idx += suffix.len;
                return .{ .start = start, .end = idx, .arg_bounds = &arg_bounds };
            }
        } else {
            idx += 1;
        }
    }

    return null;
}

pub fn main() void {}

test "zero arg parsing" {
    std.debug.print("Entering zero arg test suite...\n", .{});
    const test_input: []const u8 = "abcdef()hijkl";
    const bounds = findExpr("f(", ")", 0, test_input).?;
    try std.testing.expect(bounds.start == 5 and bounds.end == 8);
    try std.testing.expect(bounds.arg_bounds.len == 0);
}

test "single arg parsing" {
    std.debug.print("Entering single arg test suite...\n", .{});
    const test_input: []const u8 = "abcdef(123)hijkl";
    const bounds = findExpr("f(", ")", 1, test_input).?;
    try std.testing.expect(bounds.start == 5 and bounds.end == 11);
    try std.testing.expect(bounds.arg_bounds.len == 1);
    for (0..bounds.arg_bounds.len) |idx| {
        std.debug.print("{d}: start: {d}, end: {d}\n", .{ idx, bounds.arg_bounds[idx].start, bounds.arg_bounds[idx].end });
    }
    try std.testing.expect(bounds.arg_bounds[0].start == 7 and bounds.arg_bounds[0].end == 10);
}

test "double arg parsing - sane example" {
    std.debug.print("Entering double arg (sane) test suite...\n", .{});
    const test_input: []const u8 = "abcdef(123,456)hijkl";
    const bounds = findExpr("f(", ")", 2, test_input).?;
    try std.testing.expect(bounds.start == 5 and bounds.end == 15);
    try std.testing.expect(bounds.arg_bounds.len == 2);

    for (0..bounds.arg_bounds.len) |idx| {
        std.debug.print("{d}: start: {d}, end: {d}\n", .{ idx, bounds.arg_bounds[idx].start, bounds.arg_bounds[idx].end });
    }

    try std.testing.expect(bounds.arg_bounds[0].start == 7 and bounds.arg_bounds[0].end == 10);
    try std.testing.expect(bounds.arg_bounds[1].start == 11 and bounds.arg_bounds[1].end == 14);
}

test "double arg parsing - insane example" {
    std.debug.print("Entering double arg (insane) test suite...\n", .{});
    const test_input: []const u8 = "abcdef(123,,456)hijkl";
    try std.testing.expect(findExpr("f(", ")", 2, test_input) == null);
}
