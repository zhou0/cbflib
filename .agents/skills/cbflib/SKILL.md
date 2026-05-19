```markdown
# cbflib Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill provides guidance for contributing to the `cbflib` TypeScript codebase. It covers established coding conventions, testing patterns, and common workflows—especially around maintaining build stability and addressing CI failures. Use this as a reference for consistent code style, troubleshooting, and automation within the repository.

## Coding Conventions

- **File Naming:**  
  Use `snake_case` for all file names.  
  _Example:_  
  ```
  my_module.ts
  utils/helpers.ts
  ```

- **Import Style:**  
  Use **relative imports** for referencing modules within the codebase.  
  _Example:_  
  ```typescript
  import { parseData } from './parser';
  import { calculateSum } from '../math/sum';
  ```

- **Export Style:**  
  Use **named exports** rather than default exports.  
  _Example:_  
  ```typescript
  // In math_utils.ts
  export function add(a: number, b: number): number {
    return a + b;
  }

  // In another file
  import { add } from './math_utils';
  ```

- **Commit Messages:**  
  - Freeform, no strict prefix required.
  - Average length: ~65 characters.
  - _Example:_  
    ```
    Fix image conversion for 16-bit grayscale input
    Update CMakeLists.txt for optional zlib support
    ```

## Workflows

### ci-build-failure-fix
**Trigger:** When CI builds fail due to deprecations, missing dependencies, or platform-specific issues.  
**Command:** `/fix-ci-build`

1. **Identify the cause** of the CI build failure (e.g., deprecated function, missing library, or optional toolchain component).
2. **Update source code** to replace deprecated or problematic functions.  
   _Example:_  
   ```c
   // Before (deprecated)
   mktemp(template);
   // After (replacement)
   mkstemp(template);
   ```
3. **Modify `CMakeLists.txt`** to adjust build options, add or remove dependencies, and make components optional as needed.
4. **Explicitly link required libraries** (e.g., `libm`) in `CMakeLists.txt` to resolve linkage errors.
5. **Update CI workflow files** (e.g., `.github/workflows/cmake-multi-platform.yml`) to ensure required tools are installed on all platforms.
6. **Remove obsolete or deprecated build artifacts** (e.g., `Makefile_old`).

**Files Involved:**
- `CMakeLists.txt`
- `examples/convert_image.c`
- `.github/workflows/cmake-multi-platform.yml`
- `Makefile_old`

**Frequency:** ~2x/month

## Testing Patterns

- **Test File Naming:**  
  Test files follow the pattern `*.test.*` (e.g., `parser.test.ts`).

- **Testing Framework:**  
  The specific framework is not detected, but tests are likely colocated with source files or in a dedicated test directory.

- **Example Test File:**  
  ```typescript
  // parser.test.ts
  import { parseData } from './parser';

  describe('parseData', () => {
    it('should parse valid input', () => {
      expect(parseData('42')).toBe(42);
    });
  });
  ```

## Commands
| Command       | Purpose                                             |
|---------------|-----------------------------------------------------|
| /fix-ci-build | Run the CI build failure fix workflow as described. |
```
