# Compiler
CXX := g++
# Compiler flags
CXXFLAGS := -std=c++17  -Wno-int-to-pointer-cast -fpermissive

# Include directories
INCLUDES := -I ../easy/include \
            -I ../easy/lib/alice/include \
            -I ../easy/lib/any \
            -I ../easy/lib/bill/bill/include \
            -I ../easy/lib/cli11 \
            -I ../easy/lib/fmt \
            -I ../easy/lib/json/include \
            -I ../easy/lib/kitty/include \
            -I ../easy/lib/lorina \
            -I ../easy/lib/rang

# Output executable name
TARGET := esop.exe

# Source files (add more if needed)
SRCS := main.cpp

# Object files (automatically generated from source files)
OBJS := $(SRCS:.cpp=.o)

# Default target
all: $(TARGET)

# Linking the target executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $^ -o $@

# Compile source files into object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Clean rule to remove generated files
clean:
	@if exist $(OBJS) del $(OBJS)
	@if exist $(TARGET) del $(TARGET)

# Run the executable
run: $(TARGET)
	./$(TARGET)

# Phony targets (targets that are not actual files)
.PHONY: all clean run
