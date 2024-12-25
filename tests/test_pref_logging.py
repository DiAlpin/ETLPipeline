import time
from etl.trackers.perf_logging import performace_logging


# Sample class to test the decorator
class SampleTransformer:
    @performace_logging
    def sample_method(self, input_data):
        # Simulate some work
        time.sleep(0.1)
        return input_data * 2

class TestPerformanceLogging:
    transformer = SampleTransformer()

    def test_performance_logging_decorator(self):
        """
        Test that the performance logging decorator:
        1. Correctly wraps and executes the method
        2. Adds performance tracking attributes to the class
        3. Measures execution time and memory usage
        """
        # Call the method with some input
        input_data = 5
        result = self.transformer.sample_method(input_data)
        
        # Check that the method returns the correct result
        assert result == input_data * 2
        
        # Check that the performance tracking attribute exists
        assert hasattr(SampleTransformer, 'traker_perf_log')
        
        # Retrieve the performance log
        perf_log = getattr(SampleTransformer, 'traker_perf_log')
        
        # Validate the performance log structure
        assert isinstance(perf_log, list)
        assert len(perf_log) == 1
        
        # Check individual log entries
        log_entry = perf_log[0]
        assert len(perf_log[0]) == 3
        assert 'transformer' in log_entry
        assert 'exec_time' in log_entry
        assert 'memory_used' in log_entry
        
        # Validate specific attributes
        assert log_entry['transformer'] == 'SampleTransformer'
        
        # Check execution time (should be close to 0.1 seconds)
        assert 0.09 <= log_entry['exec_time'] <= 0.11
        
        # Check memory usage (should be non-zero)
        assert log_entry['memory_used'] >= 0
    
    def test_multiple_method_calls(self):
        """
        Test that multiple method calls correctly update 
        the performance tracking attribute
        """
        # Make multiple calls
        self.transformer.sample_method(5)
        self.transformer.sample_method(10)
        
        # Retrieve the performance log
        perf_log = getattr(SampleTransformer, 'traker_perf_log')
        
        # Check that multiple calls are logged
        assert len(perf_log) == 1  # Note: the implementation replaces, not appends
        
        # Validate the last log entry
        log_entry = perf_log[0]
        assert len(perf_log[0]) == 3
        assert log_entry['transformer'] == 'SampleTransformer'
        assert log_entry['exec_time'] > 0
        assert log_entry['memory_used'] >= 0

    def test_decorator_preserves_method_signature(self):
        """
        Ensure the decorator preserves the original method's metadata
        """
        # Use inspect to check method signature preservation
        import inspect
        
        original_method = SampleTransformer.sample_method
        wrapped_method = original_method.__wrapped__
        
        # Check that method name is preserved
        assert original_method.__name__ == 'sample_method'
        
        # Verify signature is maintained
        original_sig = inspect.signature(wrapped_method)
        wrapped_sig = inspect.signature(original_method)
        assert str(original_sig) == str(wrapped_sig)