"""Unit tests for plate packing algorithm."""

import unittest
from utils.plates import pack_plates


class TestPlatePacking(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.standard_lb_plates = {
            45: 2, 35: 2, 25: 2, 15: 2, 10: 2, 5: 2, 2.5: 2
        }
        
        self.standard_kg_plates = {
            25: 2, 20: 2, 15: 2, 10: 2, 5: 2, 2.5: 2, 1.25: 2
        }
    
    def test_225_lb_standard_plates(self):
        """Test 225 lb with standard plates (should be 45+45+5+2.5 per side)."""
        # 225 total - 45 bar = 180 plate weight = 90 per side
        target_per_side = 90.0
        plates, achieved, delta = pack_plates(target_per_side, self.standard_lb_plates)
        
        # Should achieve exactly 90 lb per side
        self.assertEqual(achieved, 90.0)
        self.assertEqual(delta, 0.0)
        
        # Should use 2x45, 1x5, 1x2.5 per side
        expected_plates = [(45, 2), (5, 1), (2.5, 1)]
        self.assertEqual(plates, expected_plates)
    
    def test_315_lb_standard_plates(self):
        """Test 315 lb with standard plates (should be 45+45+45+25 per side)."""
        # 315 total - 45 bar = 270 plate weight = 135 per side
        target_per_side = 135.0
        plates, achieved, delta = pack_plates(target_per_side, self.standard_lb_plates)
        
        # Should achieve exactly 135 lb per side
        self.assertEqual(achieved, 135.0)
        self.assertEqual(delta, 0.0)
        
        # Should use 2x45, 1x25, 1x15, 1x5 per side (or similar combination)
        total_weight = sum(weight * count for weight, count in plates)
        self.assertEqual(total_weight, 135.0)
    
    def test_impossible_target(self):
        """Test target that's impossible with available plates."""
        target_per_side = 500.0  # Way more than possible
        plates, achieved, delta = pack_plates(target_per_side, self.standard_lb_plates)
        
        # Should return best possible solution
        self.assertLess(achieved, target_per_side)
        self.assertLess(delta, 0)  # Should be under target
    
    def test_zero_target(self):
        """Test zero target weight."""
        target_per_side = 0.0
        plates, achieved, delta = pack_plates(target_per_side, self.standard_lb_plates)
        
        self.assertEqual(plates, [])
        self.assertEqual(achieved, 0.0)
        self.assertEqual(delta, 0.0)
    
    def test_prefer_over_option(self):
        """Test prefer over target option."""
        # Target that can't be achieved exactly
        target_per_side = 47.0  # Between 45 and 50
        
        # Test prefer under (default)
        plates_under, achieved_under, delta_under = pack_plates(
            target_per_side, self.standard_lb_plates, prefer_over=False
        )
        
        # Test prefer over
        plates_over, achieved_over, delta_over = pack_plates(
            target_per_side, self.standard_lb_plates, prefer_over=True
        )
        
        # Should get different results
        self.assertNotEqual(achieved_under, achieved_over)
    
    def test_kg_plates(self):
        """Test with kg plates."""
        # 100 kg total - 20 kg bar = 80 kg plate weight = 40 kg per side
        target_per_side = 40.0
        plates, achieved, delta = pack_plates(target_per_side, self.standard_kg_plates)
        
        # Should achieve close to 40 kg per side
        self.assertAlmostEqual(achieved, 40.0, delta=2.5)
        
        # Should be a reasonable solution
        total_weight = sum(weight * count for weight, count in plates)
        self.assertEqual(total_weight, achieved)


if __name__ == "__main__":
    unittest.main()
